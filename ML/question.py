import itertools
import logging
from typing import Optional, Dict, Union

from nltk import sent_tokenize

import torch
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizer,
)

logger = logging.getLogger(__name__)


class QGPipeline:
    """Poor man's QG pipeline"""

    def __init__(
        self,
        model: PreTrainedModel,
        tokenizer: PreTrainedTokenizer,
        ans_model: PreTrainedModel,
        ans_tokenizer: PreTrainedTokenizer,
        qg_format: str,
        use_cuda: bool,
    ):
        self.model = model
        self.tokenizer = tokenizer

        self.ans_model = ans_model
        self.ans_tokenizer = ans_tokenizer

        self.qg_format = qg_format

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

        if self.ans_model is not self.model:
            self.ans_model.to(self.device)

        assert self.model.__class__.__name__ in ["T5ForConditionalGeneration", "BartForConditionalGeneration"]

        if "T5ForConditionalGeneration" in self.model.__class__.__name__:
            self.model_type = "t5"
        else:
            self.model_type = "bart"

    def __call__(self, inputs: str):
        inputs = " ".join(inputs.split())
        sents, answers = self._extract_answers(inputs)
        flat_answers = list(itertools.chain(*answers))

        if len(flat_answers) == 0:
            return []

        if self.qg_format == "prepend":
            qg_examples = self._prepare_inputs_for_qg_from_answers_prepend(inputs, answers)
        else:
            qg_examples = self._prepare_inputs_for_qg_from_answers_hl(sents, answers)

        qg_inputs = [example["source_text"] for example in qg_examples]
        questions = self._generate_questions(qg_inputs)
        output = [{"answer": example["answer"], "question": que} for example, que in zip(qg_examples, questions)]
        return output

    def _generate_questions(self, inputs):
        inputs = self._tokenize(inputs, padding=True, truncation=True)

        outs = self.model.generate(
            input_ids=inputs["input_ids"].to(self.device),
            attention_mask=inputs["attention_mask"].to(self.device),
            max_length=32,
            num_beams=4,
        )

        questions = [self.tokenizer.decode(ids, skip_special_tokens=True) for ids in outs]
        return questions

    def _extract_answers(self, context):
        sents, inputs = self._prepare_inputs_for_ans_extraction(context)
        inputs = self._tokenize(inputs, padding=True, truncation=True)

        outs = self.ans_model.generate(
            input_ids=inputs["input_ids"].to(self.device),
            attention_mask=inputs["attention_mask"].to(self.device),
            max_length=32,
        )

        dec = [self.ans_tokenizer.decode(ids, skip_special_tokens=False) for ids in outs]
        answers = [item.split("<sep>") for item in dec]
        answers = [i[:-1] for i in answers]

        return sents, answers

    def _tokenize(self, inputs, padding=True, truncation=True, add_special_tokens=True, max_length=512):
        inputs = self.tokenizer.batch_encode_plus(
            inputs,
            max_length=max_length,
            add_special_tokens=add_special_tokens,
            truncation=truncation,
            padding="max_length" if padding else False,
            pad_to_max_length=padding,
            return_tensors="pt",
        )
        return inputs

    def _prepare_inputs_for_ans_extraction(self, text):
        sents = sent_tokenize(text)

        inputs = []
        for i in range(len(sents)):
            source_text = "extract answers:"
            for j, sent in enumerate(sents):
                if i == j:
                    sent = "<hl> %s <hl>" % sent
                source_text = "%s %s" % (source_text, sent)
                source_text = source_text.strip()

            if self.model_type == "t5":
                source_text = source_text + " </s>"
            inputs.append(source_text)

        return sents, inputs

    def _prepare_inputs_for_qg_from_answers_hl(self, sents, answers):
        inputs = []
        for i, answer in enumerate(answers):
            if len(answer) == 0:
                continue
            for answer_text in answer:
                sent = sents[i]
                sents_copy = sents[:]

                answer_text = answer_text.strip()

                ans_start_idx = sent.index(answer_text)

                sent = f"{sent[:ans_start_idx]} <hl> {answer_text} <hl> {sent[ans_start_idx + len(answer_text): ]}"
                sents_copy[i] = sent

                source_text = " ".join(sents_copy)
                source_text = f"generate question: {source_text}"
                if self.model_type == "t5":
                    source_text = source_text + " </s>"

                inputs.append({"answer": answer_text, "source_text": source_text})

        return inputs

    def _prepare_inputs_for_qg_from_answers_prepend(self, context, answers):
        flat_answers = list(itertools.chain(*answers))
        examples = []
        for answer in flat_answers:
            source_text = f"answer: {answer} context: {context}"
            if self.model_type == "t5":
                source_text = source_text + " </s>"

            examples.append({"answer": answer, "source_text": source_text})
        return examples


class MultiTaskQAQGPipeline(QGPipeline):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, inputs: Union[Dict, str]):
        if type(inputs) is str:

            return super().__call__(inputs)
        else:

            return self._extract_answer(inputs["question"], inputs["context"])

    def _prepare_inputs_for_qa(self, question, context):
        source_text = f"question: {question}  context: {context}"
        if self.model_type == "t5":
            source_text = source_text + " </s>"
        return source_text

    def _extract_answer(self, question, context):
        source_text = self._prepare_inputs_for_qa(question, context)
        inputs = self._tokenize([source_text], padding=False)

        outs = self.model.generate(
            input_ids=inputs["input_ids"].to(self.device),
            attention_mask=inputs["attention_mask"].to(self.device),
            max_length=16,
        )

        answer = self.tokenizer.decode(outs[0], skip_special_tokens=True)
        return answer


        
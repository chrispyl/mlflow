from dataclasses import dataclass
from typing import Dict, List

from mlflow.utils.annotations import experimental


@experimental
@dataclass
class MetricValue:
    """
    The value of a metric.

    :param scores: The value of the metric per row
    :param justifications: The justification (if applicable) for the respective score
    :param aggregate_results: A dictionary mapping the name of the aggregation to its value
    """

    scores: List[float] = None
    justifications: List[float] = None
    aggregate_results: Dict[str, float] = None


@experimental
@dataclass
class EvaluationExample:
    """
    Stores the sample example during few shot learning during LLM evaluation

    :param input: The input provided to the model
    :param output: The output generated by the model
    :param score: The score given by the evaluator
    :param justification: The justification given by the evaluator
    :param grading_context: The grading_context provided to the evaluator for evaluation

    .. testcode:: python
        :caption: Example for creating an EvaluationExample

        from mlflow.metrics.base import EvaluationExample

        example = EvaluationExample(
            input="What is MLflow?",
            output="MLflow is an open-source platform for managing machine "
            "learning workflows, including experiment tracking, model packaging, "
            "versioning, and deployment, simplifying the ML lifecycle.",
            score=4,
            justification="The definition effectively explains what MLflow is "
            "its purpose, and its developer. It could be more concise for a 5-score.",
            grading_context={
                "ground_truth": "MLflow is an open-source platform for managing "
                "the end-to-end machine learning (ML) lifecycle. It was developed by Databricks, "
                "a company that specializes in big data and machine learning solutions. MLflow is "
                "designed to address the challenges that data scientists and machine learning "
                "engineers face when developing, training, and deploying machine learning models."
            },
        )
        print(str(example))

    .. code-block:: text
        :caption: Output

        Input: What is MLflow?
        Provided output: "MLflow is an open-source platform for managing machine "
            "learning workflows, including experiment tracking, model packaging, "
            "versioning, and deployment, simplifying the ML lifecycle."
        Provided ground_truth: "MLflow is an open-source platform for managing "
            "the end-to-end machine learning (ML) lifecycle. It was developed by Databricks, "
            "a company that specializes in big data and machine learning solutions. MLflow is "
            "designed to address the challenges that data scientists and machine learning "
            "engineers face when developing, training, and deploying machine learning models."
        Score: 4
        Justification: "The definition effectively explains what MLflow is "
            "its purpose, and its developer. It could be more concise for a 5-score."
    """

    input: str
    output: str
    score: float
    justification: str
    grading_context: Dict[str, str] = None

    def _format_grading_context(self):
        return "\n".join(
            [f"key: {key}\nvalue:\n{value}" for key, value in self.grading_context.items()]
        )

    def __str__(self) -> str:
        grading_context = (
            ""
            if self.grading_context is None
            else "Additional information used by the model:\n" f"{self._format_grading_context()}"
        )

        return f"""
Input:
{self.input}

Output:
{self.output}

{grading_context}

score: {self.score}
justification: {self.justification}
        """

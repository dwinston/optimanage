from abc import ABC, abstractmethod


class Objective(ABC):
    """
    Abstract class for an objective for an optimization loop.
    """

    def __init__(self, model, wflows):
        """
        Creates an objective.
        """
        self._model = model
        self._wflows = wflows

    @property
    def wflows(self):
        """
        Returns a set of workflow types that are needed for this objective
        """
        return self._wflows

    @abstractmethod
    def store_model(self, store):
        """
        Serializes the model and stores in external store

        Args:
            store (Store): Location to store the model
        """
        pass

    @abstractmethod
    def load_model(self, store):
        """
        Loads model from external store.
        Args:
            store (Store): Location to load the model from
        """
        pass

    @abstractmethod
    def return_scores(self, candidates):
        """
        Returns a score for every material in the design_space.
        Stores this somewhere?

        Args:
            candidates (Set[string]): MP-ids for materials to score

        Returns:
            scores (Dict[string:float]): mapping from MP-ids to scores
        """
        pass


class HighDuctilityObjective(Objective):
    """
    Toy example of objective looking for materials with high ductility.
    Ductility is modeled using Pugh's ratio: K/G
    """

    def __init__(self, model=None, wflows=None):
        self._model = model
        self._wflows = wflows

    def model_input_property_names(self):
        return set("pretty_formula")

    def model_response_property_names(self):
        return set("elasticity.elastic_tensor")

    def return_scores(self, candidates):
        return [self.score(self._model.predict(input),
                           self._model.prediction_variance(input))
                for input in candidates]

    def score(self, prediction, uncertainty):
        return prediction

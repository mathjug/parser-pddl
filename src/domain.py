from pddl import parse_domain
from src import Object, Predicate, Action, Proposition
from typing import List, Tuple, Union

class Domain:
    """Represents a PDDL domain.

    Attributes:

    Examples:
        >>> parsed_domain = parse_domain("tests/examples/gripper3.pddl")
        >>> domain = Domain(parsed_domain)
    """

    def __init__(self, parsed_domain) -> None:
        """Initializes a 'Domain' object.

        parsed_domain: The parsed domain description, as returned by 'pddl.parse_domain'.
        """
        self.constants = self.__store_constants(parsed_domain)
        self.predicates = self.__store_predicates(parsed_domain)
        self.actions, self.pred_to_actions = self.__store_actions(parsed_domain, self.predicates)

    def __store_actions(self, parsed_domain,
                            stored_predicates: dict[str, Predicate]) -> tuple[list[Action], dict[Predicate, list[Action]]]:
        """Builds a list of actions, along with a mapping from the predicates into a list of actions
            they are associated with, i.e., each action in the list has a precondition containing the predicate.

        Args:
            parsed_domain: The parsed domain description.
            stored_predicates: A mapping from the name of the predicates to the 'Predicate' objects.

        Returns:
            list[Action]: The list of actions of the corresponding PDDL domain.
            dict[Predicate, list[Action]]): A mapping from predicates into the actions they are associated with.
        """
        actions = []
        pred_to_actions = {}
        for parsed_action in parsed_domain.actions:
            action = self.__build_action_instance(parsed_action, stored_predicates)
            actions.append(action)
            pred_to_actions = self.__store_actions_by_preconditions(action, pred_to_actions)
        return actions, pred_to_actions

    def __build_action_instance(self, parsed_action, stored_predicates: dict[str, Predicate]) -> Action:
        """Sets attributes, and builds an 'Action' object.

        Args:
            parsed_action: The parsed action description.
            stored_predicates: A mapping from the name of the predicates to the 'Predicate' objects.

        Returns:
            Action: The instantiated action.
        """
        action_name = parsed_action.name
        parameters = self.__process_action_arguments(parsed_action)
        preconditions = self.__store_preconditions_of_action(parsed_action, stored_predicates)
        all_possible_effects = []
        action_effect = parsed_action.effect
        self.__store_effects_of_action(action_effect, stored_predicates, all_possible_effects)
        effects = self.__merge_effects(all_possible_effects)
        action = Action(action_name, parameters, preconditions, effects)
        return action

    def __process_action_arguments(self, parsed_action) -> list[Object]:
        """Builds the list of arguemnts for the Action

        Args:
            parsed_action: The parsed action description.

        Returns:
            list[Object]: The list of arguments for the action.
        """
        parameters = []
        action_arguments = parsed_action.parameters
        for argument in action_arguments:
            object = self.__build_object_instance(argument)
            parameters.append(object)
        return parameters

    def __build_object_instance(self, parsed_object) -> Object:
        """Sets attributes, and build an 'Object' instance.

        Args:
            parsed_action: The parsed object description.

        Returns:
            Object: The instantiated object.
        """
        object_name = parsed_object.name
        object_type = str(next(iter(parsed_object.type_tags)))
        object = Object(object_name, object_type)
        return object

    def __store_actions_by_preconditions(self, action: Action,
                                            pred_to_actions: dict[Predicate, list[Action]]) -> dict[Predicate, list[Action]]:
        """Updates 'pred_to_actions', which is a mapping from predicates to the actions
            containing them in their preconditions.

        Args:
            action: An 'Action' object.
            pred_to_actions: A mapping from predicates into the actions they are associated with.

        Returns:
            dict[str, Predicate]: The updated mapping.
        """
        preconditions = action.get_preconditions()
        for precondition in preconditions:
            precondition_predicate = precondition[0].get_predicate()
            if precondition_predicate not in pred_to_actions:
                pred_to_actions[precondition_predicate] = []
            pred_to_actions[precondition_predicate].append(action)
        return pred_to_actions

    def __store_preconditions_of_action(self, action,
                                            stored_predicates: dict[str, Predicate]) -> list[tuple[Proposition, bool]]:
        """Builds a list of preconditions for an action.

        Args:
            action: The parsed action description.
            stored_predicates: A mapping from the name of the predicates to the 'Predicate' objects.

        Returns:
            list[tuple[Proposition, bool]]: A list of propositions, and their respective values.
        """
        if hasattr(action.precondition, "operands"): # multiple preconditions
            preconditions = action.precondition.operands
        else:
            preconditions = [action.precondition]
        processed_preconditions = []
        for precondition in preconditions:
            proposition_with_bool = self.__store_one_effect_or_precondition_predicate(precondition, stored_predicates)
            processed_preconditions.append(proposition_with_bool)
        return processed_preconditions

    def __store_effects_of_action(self, action_effects, stored_predicates: dict[str, Predicate],
                                    all_possible_effects: list[Union[list[tuple[Proposition, bool]], tuple[Proposition, bool]]] = []) -> None:
        """Builds a list of all possible effects for an action, both determinitisc and non-deterministic ones.

        Args:
            action_effects: The parsed action effects description.
            stored_predicates: A mapping from the name of the predicates to the 'Predicate' objects.
            all_possible_effects: list of deterministic and non-deterministic effects.

        Base case:
            If there is only one effect (an 'atomic' effect), stores the tuple correspoding to it in 'all_possible_effects'.

        Recursive case:
            Otherwise, the effect is either
                - 'And' effect: for each possible effect, calls the function recursively, using the current 'all_possible_effects' list; or
                - 'OneOf' effect: for each possible effect, calls the function recursively, using an empty list as 'all_possible_effects'.
        """
        effects_type = str(type(action_effects))
        if not hasattr(action_effects, "operands"):
            proposition_with_value = self.__store_one_effect_or_precondition_predicate(action_effects, stored_predicates)
            all_possible_effects.append(proposition_with_value)
            return
        if effects_type == "<class 'pddl.logic.base.OneOf'>":
            non_deterministic_effect = []
            for possible_effect in action_effects.operands:
                scenario = []
                self.__store_effects_of_action(possible_effect, stored_predicates, scenario)
                non_deterministic_effect.append(scenario)
            all_possible_effects.append(non_deterministic_effect)
        else:
            for possible_effect in action_effects.operands:
                self.__store_effects_of_action(possible_effect, stored_predicates, all_possible_effects)

    def __merge_effects(self,
                        all_possible_effects: list[Union[list[tuple[Proposition, bool]], tuple[Proposition, bool]]]) -> list[list[tuple[Proposition, bool]]]:
        """Builds a list with all possible effects, i.e., combines the deterministic
            effects with the non-deterministic ones.

        Args:
            all_possible_effects: A list with deterministic effects and the non-deterministic ones.

        Returns:
            list[list[tuple[Proposition, bool]]]: A list with the merged effects, i.e., the deterministic effects plus the non-deterministic ones

        Note:
            This method assumes that there is no 'OneOf' chain, so the 'depth' of the possibility tree is at most 2.
        """
        deterministic_effects = []
        non_deterministic_effects = []
        for effect in all_possible_effects:
            if type(effect) == list:
                for effect_scenario in effect:
                    non_deterministic_effects.append(effect_scenario)
            else:
                deterministic_effects.append(effect)
        if(len(non_deterministic_effects) == 0):
            return deterministic_effects
        effects = []
        for effect in non_deterministic_effects:
            effects.append(effect + deterministic_effects)
        return effects

    def __store_one_effect_or_precondition_predicate(self, pred, stored_predicates: dict[str, Predicate]) -> tuple[Proposition, bool]:
        pred, bool_value = self.__get_predicate_and_boolean_value(pred)
        predicate = stored_predicates[pred.name]
        objects = []
        for parsed_object in pred.terms:
            object = self.__build_object_instance(parsed_object)
            objects.append(object)
        proposition = Proposition(predicate, objects)
        proposition_with_bool = (proposition, bool_value)
        return proposition_with_bool

    def __get_predicate_and_boolean_value(self, proposition):
        bool_value = True
        if str(type(proposition)) == "<class 'pddl.logic.base.Not'>":
            bool_value = False
            proposition = proposition.argument
        return proposition, bool_value

    def __store_constants(self, parsed_domain) -> dict[str, Object]:
        dict_const = {}
        for parsed_constant in parsed_domain.constants:
            constant_type = str(next(iter(parsed_constant.type_tags)))
            if constant_type not in dict_const:
                dict_const[constant_type] = []
            constant_name = parsed_constant.name
            constant = Object(constant_name, constant_type)
            dict_const[constant_type].append(constant)
        return dict_const

    def __store_predicates(self, parsed_domain) -> dict[str, Predicate]:
        predicates = {}
        for predicate in parsed_domain.predicates:
            variable_types = []
            for object in predicate.terms:
                variable_types.append(str(next(iter(object.type_tags))))
            predicate_object = Predicate(predicate.name, variable_types)
            predicates[predicate.name] = predicate_object
        return predicates

    def get_constants(self) -> dict[str, Object]:
        return self.constants

    def get_predicates(self) -> dict[str, Predicate]:
        return self.predicates

    def get_actions(self) -> list[Action]:
        return self.actions

    def get_pred_to_actions(self) -> dict[Predicate, list[Action]]:
        return self.pred_to_actions
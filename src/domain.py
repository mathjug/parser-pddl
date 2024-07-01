from pddl import parse_domain
from src import Object, Predicate, Action, Proposition

class Domain:
    def __init__(self, parsed_domain):
        self.constants = self.__store_constants(parsed_domain)
        self.predicates = self.__store_predicates(parsed_domain)
        self.actions, self.pred_to_actions = self.__store_actions(parsed_domain, self.predicates)

    def __store_actions(self, parsed_domain, stored_predicates):
        actions = []
        pred_to_actions = {}
        for parsed_action in parsed_domain.actions:
            action = self.__build_action_instance(parsed_action, stored_predicates)
            actions.append(action)
            pred_to_actions = self.__store_actions_by_preconditions(action, pred_to_actions)
        return actions, pred_to_actions

    def __build_action_instance(self, parsed_action, stored_predicates):
        action_name = parsed_action.name
        parameters = self.__process_action_arguments(parsed_action)
        preconditions = self.__store_preconditions_of_action(parsed_action, stored_predicates)
        all_possible_effects = []
        action_effect = parsed_action.effect
        self.__store_effects_of_action(action_effect, stored_predicates, all_possible_effects)
        effects = self.__merge_effects(all_possible_effects)
        action = Action(action_name, parameters, preconditions, effects)
        return action

    def __process_action_arguments(self, action):
        parameters = []
        action_arguments = action.parameters
        for argument in action_arguments:
            object = self.__build_object_instance(argument)
            parameters.append(object)
        return parameters

    def __build_object_instance(self, parsed_object):
        object_name = parsed_object.name
        object_type = str(next(iter(parsed_object.type_tags)))
        object = Object(object_name, object_type)
        return object

    def __store_actions_by_preconditions(self, action, pred_to_actions):
        preconditions = action.get_preconditions()
        for precondition in preconditions:
            precondition_predicate = precondition[0].get_predicate()
            if precondition_predicate not in pred_to_actions:
                pred_to_actions[precondition_predicate] = []
            pred_to_actions[precondition_predicate].append(action)
        return pred_to_actions

    def __store_preconditions_of_action(self, action, stored_predicates):
        if hasattr(action.precondition, "operands"): # multiple preconditions
            preconditions = action.precondition.operands
        else:
            preconditions = [action.precondition]
        processed_preconditions = []
        for precondition in preconditions:
            proposition_with_bool = self.__store_one_effect_or_precondition_predicate(
                                            precondition, stored_predicates)
            processed_preconditions.append(proposition_with_bool)
        return processed_preconditions

    def __store_effects_of_action(self, action_effects, stored_predicates, all_possible_effects = []):
        effects_type = str(type(action_effects))
        if not hasattr(action_effects, "operands"):
            proposition_with_value = self.__store_one_effect_or_precondition_predicate(
                                                action_effects, stored_predicates)
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
                self.__store_effects_of_action(possible_effect, stored_predicates,
                                                                all_possible_effects)

    def __merge_effects(self, effects):
        deterministic_effects = []
        non_deterministic_effects = []
        for effect in effects:
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

    def __store_one_effect_or_precondition_predicate(self, pred, stored_predicates):
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

    def __store_constants(self, parsed_domain):
        dict_const = {}
        for parsed_constant in parsed_domain.constants:
            constant_type = str(next(iter(parsed_constant.type_tags)))
            if constant_type not in dict_const:
                dict_const[constant_type] = []
            constant_name = parsed_constant.name
            constant = Object(constant_name, constant_type)
            dict_const[constant_type].append(constant)
        return dict_const

    def __store_predicates(self, parsed_domain):
        predicates = {}
        for predicate in parsed_domain.predicates:
            variable_types = []
            for object in predicate.terms:
                variable_types.append(str(next(iter(object.type_tags))))
            predicate_object = Predicate(predicate.name, variable_types)
            predicates[predicate.name] = predicate_object
        return predicates

    def get_constants(self):
        return self.constants

    def get_predicates(self):
        return self.predicates

    def get_actions(self):
        return self.actions

    def get_pred_to_actions(self):
        return self.pred_to_actions
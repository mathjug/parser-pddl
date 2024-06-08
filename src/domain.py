from pddl import parse_domain
from custom_types import Object, Predicate, Action, Proposition

class Domain:
    def __init__(self, parsed_domain):
        self.constants = self.__store_constants(parsed_domain)
        self.predicates = self.__store_predicates(parsed_domain)
        self.actions = self.__store_actions(parsed_domain, self.predicates)
    
    def __store_actions(self, parsed_domain, stored_predicates):
        dict_actions = {}
        for action in parsed_domain.actions:
            action_name = action.name
            preconditions = self.__store_preconditions_of_action(action, stored_predicates)
            all_possible_effects = self.__store_effects_of_action(action, stored_predicates)
            dict_actions[action_name] = Action(action_name, preconditions, all_possible_effects)
        return dict_actions

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
    
    def __store_effects_of_action(self, action, stored_predicates):
        action_effects = action.effect
        effects_type = str(type(action_effects))
        all_possible_effects = []

        if effects_type == "<class 'pddl.logic.effects.AndEffect'>":
            deterministic_effect = self.__store_one_effect_scenario(action_effects, stored_predicates)
            all_possible_effects.append(deterministic_effect)
        elif effects_type == "<class 'pddl.logic.base.OneOf'>":
            for possible_effect in action_effects.operands:
                non_deterministic_effect = self.__store_one_effect_scenario(possible_effect,
                                                                            stored_predicates)
                all_possible_effects.append(non_deterministic_effect)
        elif not hasattr(action_effects, "operands"):
            proposition_with_bool = self.__store_one_effect_or_precondition_predicate(
                                                action_effects, stored_predicates)
            all_possible_effects.append([proposition_with_bool])
        return all_possible_effects
    
    def __store_one_effect_or_precondition_predicate(self, pred, stored_predicates):
        pred, bool_value = self.__get_predicate_and_boolean_value(pred)
        predicate = stored_predicates[pred.name]
        objects = []
        for object in pred.terms:
            obj_name = object.name
            obj_type = str(next(iter(object.type_tags)))
            objects.append(Object(obj_name, obj_type))
        proposition = Proposition(predicate, objects)
        proposition_with_bool = (proposition, bool_value)
        return proposition_with_bool
    
    def __store_one_effect_scenario(self, action_effects, stored_predicates):
        effect_scenario = []
        for pred in action_effects.operands:
            proposition_with_bool = self.__store_one_effect_or_precondition_predicate(
                                                pred, stored_predicates)
            effect_scenario.append(proposition_with_bool)
        return effect_scenario
    
    def __get_predicate_and_boolean_value(self, proposition):
        bool_value = True
        if str(type(proposition)) == "<class 'pddl.logic.base.Not'>":
            bool_value = False
            proposition = proposition.argument
        return proposition, bool_value

    def __store_constants(self, parsed_domain):
        dict_const = {}
        for constant in parsed_domain.constants:
            constant_type = str(next(iter(constant.type_tags)))
            if constant_type not in dict_const:
                dict_const[constant_type] = []

            constant_name = repr(constant)[9:-1]
            constant = Object(constant_name, constant_type)
            dict_const[constant_type].append(constant)

        return dict_const

    def __store_predicates(self, parsed_domain):
        predicates = {}
        for predicate in parsed_domain.predicates:
            variable_types = []
            for object in predicate.terms:
                variable_types.append(str(next(iter(object.type_tags))))

            instantiated_predicate = Predicate(predicate.name, variable_types)
            predicates[predicate.name] = instantiated_predicate

        return predicates

    def get_constants(self):
        return self.constants

    def get_predicates(self):
        return self.predicates

    def get_actions(self):
        return self.actions

def main():
    domain_path = "../tests/examples/gripper3.pddl"
    parsed_domain = parse_domain(domain_path)
    domain = Domain(parsed_domain)

    print("CONSTANTS")
    constant_dict = domain.constants
    for constant_type in constant_dict:
        print(constant_type, end = ':')
        constants = constant_dict[constant_type]
        for constant in constants:
            print(f" {constant}", end = '')
        print("\n")

    print("PREDICATES")
    predicates = domain.predicates
    for predicate in predicates:
        print(predicate)

if __name__ == "__main__":
    main()
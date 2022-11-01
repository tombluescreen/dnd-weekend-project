from main import dnd_modifier, Character
from debug import dprint

class BetterModEffect:
    def __init__(self, effected_value:dnd_modifier, condition_var, value_var, label="Unlabled Effect") -> None:
        self.label = label
        self.effected_value = effected_value
        self.value_var = value_var
        self.condition_var = condition_var

    def is_valid(self) -> bool:
        return self.condition_var.__bool__()
        
    def init_effected_mod(self):
        self.effected_value.register_effect(self)

#Returns a True or False depending on value
class ModCondition:
    def __init__(self, value_get, true_object = True) -> None:
        self.value_get = value_get
        self.true_object = true_object

    def __bool__(self):
        val_get = self.value_get()
        true_get = self.true_object
        r = (val_get == true_get)
        dprint(f"ModCondition: {val_get}=={true_get}={r}",3)
        return r

class ModValue:
    def __init__(self, value_get) -> None:
        self.value_get = value_get

    def __real__(self):
        return self.value_get()

class DictRef:
    def __init__(self, di:dict, key) -> None:
        self.di = di
        self.key = key
    
    def get_value(self):
        r = self.di[self.key]
        dprint(f"DictRef: <{self.key},{r}>",3)
        return r

    def get(self):
        return self.get_value()

    def __call__(self):
        return self.get_value()



#Old Classes
class ModEffect:
    def __init__(self, _effected_value:dnd_modifier, effect_mod:int,  label = "unlabeld generic effect") -> None:
        self.label = label
        self.effected_value:dnd_modifier = _effected_value
        self._static_effect_mod = effect_mod

    def init_effected_mod(self):
        self.effected_value.register_effect(self)

    def free_effect(self):
        self.effected_value.remove_registerd_effect(self)

    def is_valid(self) -> bool:
        return True
    
    @property
    def effect_mod(self):
        return self._static_effect_mod




class ProfModEffect(ModEffect): # Could be replaced by an Attribute based solution
    def __init__(self, parent_character:Character, prof_obj, _effected_value: dnd_modifier, label="unlabeld Prof effect") -> None:
        super().__init__(_effected_value, 0, label)
        self.prof_obj = prof_obj
        self.parent_character = parent_character
    
    def is_valid(self) -> bool:
        return self.prof_obj.proficiency
    
    @property
    def effect_mod(self):
        apply_prof = self.is_valid()
        if apply_prof:
            dprint(f"{self.label} is valid - Applying +{self.parent_character.proficiency_bonus}")
            return self.parent_character.proficiency_bonus
        else:
            dprint(f"{self.label} is NOT valid")
            return 0


class AbilityScoreEffect(ModEffect): #unused
    def __init__(self, _effected_value: dnd_modifier, dict_obj:dict, dict_key:str, label="unlabeld Dict Ref effect") -> None:
        super().__init__(_effected_value, 0, label)
        self.dict_obj = dict_obj
        self.dict_key = dict_key

    def is_valid(self) -> bool:
        return True

    @property
    def effect_mod(self):
        apply_prof = self.is_valid()
        if apply_prof:
            dprint(f"{self.label} is valid - Applying +{self.dict_obj[self.dict_key].__str__()}")
            return int(self.dict_obj[self.dict_key].__str__())
        else:
            dprint(f"{self.label} is NOT valid")
            return 0
    

class DictRefEffect(ModEffect):
    def __init__(self, _effected_value: dnd_modifier, dict_obj:dict, dict_key:str, label="unlabeld Dict Ref effect") -> None:
        super().__init__(_effected_value, 0, label)
        self.dict_obj = dict_obj
        self.dict_key = dict_key

    def is_valid(self) -> bool:
        return True

    @property
    def effect_mod(self):
        apply_prof = self.is_valid()
        if apply_prof:
            obj = self.dict_obj[self.dict_key].__str__()
            dprint(f"{self.label} is valid - Applying +{self.dict_obj[self.dict_key]}")
            return int(self.dict_obj[self.dict_key].__str__())
        else:
            dprint(f"{self.label} is NOT valid")
            return 0
from math import floor
import enums as e
import effects as eff

class dnd_modifier():
    def __init__(self, value:int) -> None:
        self.value = value
        self.registerd_effects:list[eff.ModEffect] = []
        
    def calculate_with_registerd_effects(self):
        value = self.value
        for eff in self.registerd_effects:
            value += eff.effect_mod # This could be changed to include * and /
        return value

    def list_registerd_effects(self) -> list[str]:
        text = []
        for eff in self.registerd_effects:
            text.append(eff.label) # This could be changed to include * and /
        return text

    def register_effect(self, eff) -> None:
        self.registerd_effects.append(eff)

    def remove_registerd_effect(self,eff):
        self.registerd_effects.remove(eff)

    def __call__(self) -> int:
        return self.calculate_with_registerd_effects()

    def __repr__(self) -> str:
        return f"{{{self.value}, +{self.calculate_with_registerd_effects()-self.value}}}"   

    def __str__(self) -> str:
        return str(self.calculate_with_registerd_effects())

class dnd_Time:
    def __init__(self, base_time = 0) -> None:
        
        
        self.real_time = base_time
        
        


class Campaign:
    def __init__(self) -> None:
        self.label = ""
        self.realtime = ""

class Entity:
    def __init__(self) -> None:
        pass


class Item:
    def __init__(self) -> None:
        self.weight = None
        self.label = None

class Equipment(Item): #always unique
    def __init__(self) -> None:
        super().__init__()
        self.equiped: bool = False
        self.equip_effects:list[eff.ModEffect] = [] # effects when the equiment is equiped 
        self.inventory_effects:list[eff.ModEffect] = [] # effects when the equiment is unequiped 


class Weapon(Equipment):
    def __init__(self) -> None:
        super().__init__()
        self.attack_effects:list[eff.ModEffect] = [] # effects inflicted on the target

class Inventory:
    def __init__(self) -> None:
        self.items = None

class Character(Entity):
    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = None
        self.ability_scores: Ability_Scores
        self.skills:Skills
        self.proficiency_bonus = 3
        self.inspiration = False
        self.armour_class = dnd_modifier(10) #wont change until inventory is implementd
        self.initiative = dnd_modifier(10)
        self.inventory = Inventory()
        self.saving_throws:Saving_Throws
        

    def test_generate_base_stats(self):
        beans = {"strength":20,"dexterity":2,"constitution":12,"intelligence":13,"wisdom":14,"charisma":15}
        self.ability_scores = Ability_Scores(beans)

        self.skills = Attributes({"beans": Skill(self,"strength")})
        saving_throw_dict = {
            "strength": Saving_Throw(self,"Strength", "strength"),
            "dexterity": Saving_Throw(self,"Dexterity", "dexterity"),
            "constitution": Saving_Throw(self,"Constitution", "constitution"),
            "intelligence ": Saving_Throw(self,"Intelligence", "intelligence"),
            "wisdom": Saving_Throw(self,"Wisdom", "wisdom"),
            "charisma": Saving_Throw(self,"Charisma", "charisma"),
        }
        self.saving_throws = Saving_Throws(saving_throw_dict)
        

class Attributes(dict):
    def __setitem__(self, key, value) -> None:
        return super().__setitem__(key, value)

class Skill:
    def __init__(self, character: Character, mod_key:str, proficiency:bool = False) -> None:
        self.character = character
        self.proficiency:bool = proficiency
        self.mod_key = mod_key
        self.bonus:dnd_modifier = dnd_modifier(0)
        self.prof_effect_obj:eff.ProfModEffect


        self.init_prof_mod_effect()

    def init_prof_mod_effect(self):
        self.prof_effect_obj = eff.ProfModEffect(self.character,self, self.bonus)
        self.prof_effect_obj.init_effected_mod()

    #@property
    #def bonus(self) -> int:
    #    # This is the assigned ABILITY_SCORE + PROFICIENCY bonus
    #    prof_bonus = 0
    #    if self.proficiency:
    #        prof_bonus = self.character.proficiency_bonus

    #    return (self.character.ability_scores[self.mod_key].modifier + prof_bonus)


class Skills(Attributes):
    def __init__(self, args=None):
        super().__init__()
        
        if isinstance(args, dict):
            
            for x,y in args.items():
                if isinstance(y, Skill):
                    self.__setitem__(x,y)
                

    def __getitem__(self, key) -> Skill:
        return super().__getitem__(key)

    def __setitem__(self, key, value) -> None:
        return super().__setitem__(key, value)


class Ability_Score:
    def __init__(self) -> None:
        self.base_score: int


    @property
    def total_score(self) -> int:
        return self.base_score

    @property
    def modifier(self) -> int:
        return floor((self.total_score - 10)/2)

    def __str__(self) -> str:
        return str(self.modifier)


    
class Ability_Scores(Attributes):
    def __init__(self, args=None):
        super().__init__()
        
        if isinstance(args, dict):
            
            for x,y in args.items():
                if isinstance(y, Ability_Score):
                    self.__setitem__(x,y)
                elif isinstance(y,int):
                    temp = Ability_Score()
                    temp.base_score = y
                    self.__setitem__(x,temp)

    def __getitem__(self, key) -> Ability_Score:
        return super().__getitem__(key)

    def __setitem__(self, key, value) -> None:
        return super().__setitem__(key, value)

        
class Saving_Throw():
    def __init__(self, character:Character, name:str, ability_score_key:str) -> None:
        self.name = name
        self.ability_score_effect_obj = ability_score_key
        self.character = character
        self.proficiency:bool = False
        self.bonus: dnd_modifier = dnd_modifier(0)
        self.prof_effect_obj:eff.ProfModEffect
        self.ability_score_effect_obj:eff.DictRefEffect
        self.init_prof_mod_effect()

    def init_prof_mod_effect(self):
        self.prof_effect_obj = eff.ProfModEffect(self.character,self, self.bonus,f"Saving Throw {self.name} Prof")
        self.prof_effect_obj.init_effected_mod()
        self.ability_score_effect_obj = eff.DictRefEffect(self.bonus,self.character.ability_scores, self.ability_score_effect_obj, f"Saving Throw {self.name} Ability Score")
        self.ability_score_effect_obj.init_effected_mod()

class Saving_Throws(Attributes):
    def __init__(self, args=None):
        super().__init__()
        
        if isinstance(args, dict):
            
            for x,y in args.items():
                if isinstance(y, Saving_Throw):
                    self.__setitem__(x,y)

    def __getitem__(self, key) -> Saving_Throw:
        return super().__getitem__(key)

    def __setitem__(self, key, value) -> None:
        return super().__setitem__(key, value)


class Game_State:
    def __init__(self) -> None:
        self.campaign: Campaign


if __name__ == "__main__":



    

    testC = Character(None)
    testC.test_generate_base_stats()
    
    
    testMOD = dnd_modifier(0)
    testEFF = eff.DictRefEffect(testMOD, testC.ability_scores, "strength")
    testEFF.init_effected_mod()
    print(testMOD)

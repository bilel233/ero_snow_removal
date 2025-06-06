import math

class ChasseNeige:
    def __init__(self, type_camion, km=0):
        
        self.type = type_cammion

        if self.type == 1:
            cout_jour = math.ceil((km/10)/24) * 500
            cout_heure = math.ceil(math.min(km/20, 8)) * 1.1 + math.ceil(math.max(km/20 - 8, 0)) * 1.3
            cout_km = math.ceil(km) * 1.1
            self.cout = cout_jour + cout_heure + cout_km

        elif self.type == 2:
            cout_jour = math.ceil((km/10)/24) * 800
            cout_heure = math.ceil(math.min(km/20, 8)) * 1.3 + math.ceil(math.max(km/20 - 8, 0)) * 1.5
            cout_km = math.ceil(km) * 1.3
            self.cout = cout_jour + cout_heure + cout_km
        else:
            raise ValueError("Type de camion non valide. Utilisez 1 ou 2.")


def fleet_eval(nb_drone,kmDrone,list_chas_neige):
    
    vm_Drone = 70 #vitesse moyenne du drone
    ct_km_Drone = 0.01 * kmDrone
    ct_heure_Drone = math.ceil((kmDrone/20)/24 + nb_Drone) * 100
    
    Tot_Drone = ct_km_Drone + ct_jour_Drone
    Tot_T1 = 0
    Tot_T2 = 0
    
    for i in list_chas_neige:
    
        if i.type == 1:
            Tot_T1 = Tot_T1 + i.cout
        
        else:
            Tot_T2 = Tot_T2 + i.cout
            
    Tot = Tot_Drone + Tot_T1 + Tot_T2
    
    if Tot > 16000000:
        raise ValueError("Bon bah, on a mis l'Etat en banqueroute!")
    return {"cout des drones": Tot_Drone, "cout des types 1": Tot_T1, "cout des types 2": Tot_T2, "cout total": Tot_Drone + Tot_T1 + Tot_T2}

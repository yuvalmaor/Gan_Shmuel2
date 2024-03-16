
def caclc_containers_weights(containers_weights , unit):
    res = 0
    for container_weight, container_unit in containers_weights:
        if container_unit == unit:
            res += container_weight
        else:
            if container_unit == "kg": # unit = "lbs"
                res += container_weight*2.20462
            else: 
                res += container_weight*0.453592
    return res


def calc_transaction_neto(bruto, tara, containers_weight):
    return bruto-tara-containers_weight

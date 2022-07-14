from random import randint


def throw_dice(dice="d20", count_dices=1):
    """
    Функция возвращает результат бросков (count_dices - количество костей) dice (тип кости).
    """
    max_dices = 10
    if count_dices > max_dices:
        count_dices = max_dices

    match dice:
        case "d6":
            values = (randint(1, 6) for i in range(count_dices))
        case "d4":
            values = (randint(1, 4) for i in range(count_dices))
        case "d8":
            values = (randint(1, 8) for i in range(count_dices))
        case "d10":
            values = (randint(1, 10) for i in range(count_dices))
        case "d20":
            values = (randint(1, 20) for i in range(count_dices))
        case "d100":
            values = (randint(1, 100) for i in range(count_dices))

    return values

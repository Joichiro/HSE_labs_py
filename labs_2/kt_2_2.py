# Инвестпроект представляет собой интернет-магазин по продаже чая на площадке Wildberries
# Первоначальные затарты составляют 823 000 руб.
# Срок реализации 1 года
# Планируемая сумма поступлений за период 5 100 000 руб
# Затраты за период 4 950 000 руб.
# Cтавка дисконтирования 2%
import warnings
from functools import reduce
from itertools import accumulate
import numpy as np
import numpy_financial as nf
warnings.filterwarnings("ignore", category=DeprecationWarning)

initialCosts = 823000
projectDuration = 12
yearIncome = 5100000
yearConsumption = 4950000
discountRate = 0.02

# NPV
incomeByPeriods = [yearIncome] * projectDuration
outcomeByPeriods = ([yearConsumption] * projectDuration)
netValueByPeriods = list(map(lambda i, o: i - o, incomeByPeriods, outcomeByPeriods))
NPVByPeriods = list(map(lambda i: netValueByPeriods[i] / ((1 + discountRate) ** (i + 1)), range(0, projectDuration)))
NPVAccumulated = list(accumulate(NPVByPeriods))
NPV = NPVAccumulated[len(NPVAccumulated) - 1] - initialCosts
paybackPeriod = next(x for x, val in enumerate(NPVAccumulated) if val > initialCosts)
# дисконтированный срок окупаемости
DPP = paybackPeriod + (1 - ((NPVAccumulated[paybackPeriod] - initialCosts) / NPVByPeriods[paybackPeriod]))
# IRR
IRR = nf.irr([initialCosts * -1] + netValueByPeriods)

print("NPV = {0} - сумма потока платежей, приведённых к сегодняшнему дню. В нашем случае NPV положительный, "
      "значит при заданных параметрах (срок 12 месяцев, ставка дисконтирования = 2%) по итогу принесет "
      "прибыль.".format(round(NPV, 2)))
print("DPP = {0} - дисконтированный срок окупаемости проекта. В нашем случае проект окупается через {0} "
      "года, с учетом приведения потоков платежей, приведенных к сегодняшнему дню.".format(round(DPP, 2)))
print("IRR = {0} - внутренняя норма доходности, т.е. только при ставке дисконтирования = {0}% и выше наш проект "
      "сможет окупиться".format(round(IRR, 4)))
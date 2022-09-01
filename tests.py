# list = ['adxam', 'eshmat', 'toshmat', 'himmat']
# for lst in list:
from operator import indexOf
from django.core.paginator import Paginator


list = "hammaga salom bugun 1-sentabr"


lst = list.split()

p = Paginator(lst, 2)
page1 = p.page(1)
print(page1.object_list)

# k = 0
# for i in range(len(lst), 2):
#     print(i)

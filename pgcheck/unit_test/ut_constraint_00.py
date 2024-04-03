import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from pgcheck.unit_test.ut_constraint_08_like import ut_constraint_08_like
from pgcheck.unit_test.ut_constraint_09_ilike import ut_constraint_09_ilike
from pgcheck.unit_test.ut_constraint_10_similar import ut_constraint_10_similar
from pgcheck.unit_test.ut_constraint_11_between import ut_constraint_11_between
from pgcheck.unit_test.ut_constraint_12_notbetween import ut_constraint_12_notbetween
from pgcheck.unit_test.ut_constraint_15_and import ut_constraint_15_and
from pgcheck.unit_test.ut_constraint_16_or import ut_constraint_16_or
from pgcheck.unit_test.ut_constraint_17_not import ut_constraint_17_not

def ut_constraint_00():
    test_name = 'ut_constraint_00'
    result = False

    t8, r8 = ut_constraint_08_like()
    t9, r9 = ut_constraint_09_ilike()
    t10, r10 = ut_constraint_10_similar()
    t11, r11 = ut_constraint_11_between()
    t12, r12 = ut_constraint_12_notbetween()
    t15, r15 = ut_constraint_15_and()
    t16, r16 = ut_constraint_16_or()
    t17, r17 = ut_constraint_17_not()
    
    result = r8 and r9 and r10 and r11 and r12 and r15 and r16 and r17

    if result:
        print(test_name, ' ok.')

    return test_name, result

if __name__ == "__main__":
    ut_constraint_00()
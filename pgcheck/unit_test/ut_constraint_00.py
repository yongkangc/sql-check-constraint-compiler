import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from pgcheck.unit_test.ut_constraint_01_op import ut_constraint_01_op
from pgcheck.unit_test.ut_constraint_02_op_any import ut_constraint_02_op_any
from pgcheck.unit_test.ut_constraint_03_op_all import ut_constraint_03_op_all
from pgcheck.unit_test.ut_constraint_06_nullif import ut_constraint_06_nullif
from pgcheck.unit_test.ut_constraint_07_in import ut_constraint_07_in
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
    result = True


    t1, r1 = ut_constraint_01_op()
    t2, r2 = ut_constraint_02_op_any()
    t3, r3 = ut_constraint_03_op_all()
    t6, r6 = ut_constraint_06_nullif()
    t7, r7 = ut_constraint_07_in()
    t8, r8 = ut_constraint_08_like()
    t9, r9 = ut_constraint_09_ilike()
    t10, r10 = ut_constraint_10_similar()
    t11, r11 = ut_constraint_11_between()
    t12, r12 = ut_constraint_12_notbetween()
    t15, r15 = ut_constraint_15_and()
    t16, r16 = ut_constraint_16_or()
    t17, r17 = ut_constraint_17_not()
    
    result = r1 and r2 and r3 and r6 and r7 and r8 and r9 and r10 and r11 and r12 and r15 and r16 and r17

    if result:
        print(test_name, ' ok.')

    return test_name, result

if __name__ == "__main__":
    ut_constraint_00()
class Variable:
    def get_name(self):
        pass

class Assignment:
    def get_var(self) -> Variable:
        pass

    def get_value(self) -> float:
        pass

    def set_value(self, f: float):
        pass

class Assignments:
    def __getitem__(self, v: Variable) -> float:
        pass

    def __iadd__(self, ass: Assignment):
        pass

class Expression:
    def evaluate(self, assgms: Assignments) -> float:
        pass

    def derivative(self, v: Variable):
        pass

    def __repr__(self) -> str:
        pass

    def __eq__(self, other):
        pass

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __pow__(self, power: float, modulo=None):
        pass

class ValueAssignment(Assignment):
    def __init__(self, v:Variable, value:float):
        self.v=v
        self.value=Constant(value)

    def __eq__(self, other) -> bool:
        return self.v.get_name()==other.v.get_name() and self.value==other.value

    def get_var(self) -> Variable:
        return self.v

    def get_value(self) -> float:
        return self.value.get_value()

    def set_value(self, f: float):
        self.value=Constant(f)

    def __repr__(self) -> str:
        return f"{self.v}={self.value}"

class SimpleDictionaryAssignments(Assignments):
    def __init__(self):
        self.mydict = {}
    def __getitem__(self, v: Variable) -> float:
        return self.mydict[v] 
    
    def __iadd__(self, ass: Assignment):
        self.mydict.update({ass.get_var().get_name() : ass.get_value()})
        return self

class Constant(Expression):

    def __init__(self, value: float=0.0):
        self.value = value
    def evaluate(self, assgms: Assignments) -> float:
        return self.value

    def derivative(self, v: Variable):
        return float(0)

    def __repr__(self) -> str:
        return str(self.get_value())
    def get_value(self):
        return float(self.value)
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.value == other.value

    def __add__(self, other):
        return Addition(self,other)

    def __sub__(self, other):
        return Subtraction(self,other)

    def __mul__(self, other):
        return Multiplication(self,other)

    def __pow__(self, power: float, modulo=None):
        return Power(self, power)

class VariableExpression(Variable,Expression):
    def __init__(self, variable_name):
        self.variable_name=variable_name
    
    def get_name(self):
        return self.variable_name
    
    def evaluate(self, assgms: Assignments) -> float:
        return assgms[self.variable_name]

    def derivative(self, v: Variable):
        if v.get_name()==self.get_name():
            return Constant(float(1))
        return Constant(float(0))

    def __repr__(self) -> str:
        return self.variable_name

    def __eq__(self, other):
        return self.variable_name==other.variable_name

    def __add__(self, other):
        return Addition(self,other)

    def __sub__(self, other):
        return Subtraction(self,other)

    def __mul__(self, other):
        return Multiplication(self,other)

    def __pow__(self, power: float, modulo=None):
        return Power(self,power)

class Addition(Expression):
    def __init__(self, A: Expression, B: Expression):
        self.A=A
        self.B=B

    def evaluate(self, assgms: Assignments) -> float:
        return self.A.evaluate(assgms) + self.B.evaluate(assgms)        

    def derivative(self, v: Variable):
        return Addition(self.A.derivative(v), self.B.derivative(v))

    def __repr__(self) -> str:
        return f"({self.A}+{self.B})"

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        
    def __add__(self, other):
        return Addition(self,other)

    def __sub__(self, other):
        return Subtraction(self,other)

    def __mul__(self, other):
        return Multiplication(self,other)

    def __pow__(self, power: float, modulo=None):
        return Power(self,power)

class Subtraction(Expression):
    def __init__(self, A: Expression, B: Expression):
        self.A=A
        self.B=B

    def evaluate(self, assgms: Assignments) -> float:
        return self.A.evaluate(assgms) - self.B.evaluate(assgms) 

    def derivative(self, v: Variable):
        return Subtraction(self.A.derivative(v), self.B.derivative(v))

    def __repr__(self) -> str:
        return f"({self.A}-{self.B})"

    def __eq__(self, other):
        if type(self) != type(other):
            return False

    def __sub__(self, other):
        return Subtraction(self,other)

    def __add__(self, other):
        return Addition(self,other)

    def __mul__(self, other):
        return Multiplication(self,other)

    def __pow__(self, power: float, modulo=None):
        return Power(self,power)

class Multiplication(Expression):
    def __init__(self, A: Expression, B: Expression):
        self.A=A
        self.B=B
    
    def evaluate(self, assgms: Assignments) -> float:
        return self.A.evaluate(assgms) * self.B.evaluate(assgms) 

    def derivative(self, v: Variable):
        return Addition(Multiplication(self.A.derivative(v),self.B),Multiplication(
         self.A,self.B.derivative(v)))

    def __repr__(self) -> str:
        return f"({self.A}*{self.B})"

    def __eq__(self, other):
        if type(self) != type(other):
            return False

    def __mul__(self, other):
        return Multiplication(self,other)

    def __sub__(self, other):
        return Subtraction(self,other)

    def __add__(self, other):
        return Addition(self,other)

    def __pow__(self, power: float, modulo=None):
        return Power(self,power)

class Power(Expression):
    def __init__(self, exp: Expression, p: float):
        self.exp=exp
        self.p=Constant(p)

    def evaluate(self, assgms: Assignments) -> float:
        return self.exp.evaluate(assgms) ** self.p.evaluate(assgms)

    def derivative(self, v: Variable):
        return Multiplication(Multiplication(self.p,Power(self.exp,self.p.get_value()-1)),self.exp.derivative(v))

    def __repr__(self) -> str:
        return f"({self.exp}^{self.p})"


    def __eq__(self, other):
        if type(self) != type(other):
            return False

    def __mul__(self, other):
        return Multiplication(self,other)

    def __sub__(self, other):
        return Subtraction(self,other)

    def __add__(self, other):
        return Addition(self,other)

    def __pow__(self, power: float, modulo=None):
        return Power(self,power)

class Polynomial(Expression):
    def __init__(self, v: Variable, coefs: list):
        self.v=v
        self.coefs=coefs

    def evaluate(self, assgms: Assignments) -> float:
        return self.coefs[2] * Power(self.v,2).evaluate(assgms) + self.coefs[1] * self.v.evaluate(assgms) + self.coefs[0]

    def derivative(self, v: Variable):
        if self.v == v:
            if self.coefs[2]==0:
                return self.coefs[1]
            elif self.coefs[1]==0:
                return Polynomial(self.v,[0,0,2*self.coefs[2]])
            return Polynomial(self.v,[self.coefs[1],2*self.coefs[2],0])
        return float(0)


    def __repr__(self) -> str:
        first=''
        second=''
        last=''
        sign='+'
        if self.coefs[2]!=0:
            first=f"{self.coefs[2]}{self.v}^2"
        if self.coefs[1]!=0:
            second=f"{self.coefs[1]}{self.v}"
            if self.coefs[1] > 0 and self.coefs[2]!=0:
                second=f"{sign}{second}"
        if self.coefs[0]!=0:
            last=f"{self.coefs[0]}"
            if self.coefs[0] > 0 and self.coefs[1]!=0 :
                last=f"{sign}{last}"

        return "(" + first + second + last + ")"


    def __eq__(self, other):
        if type(self) != type(other):
            return False

    def __add__(self, other):
        return Addition(self,other)

    def __sub__(self, other):
        return Subtraction(self,other)

    def __mul__(self, other):
        return Multiplication(self, other)

    def __pow__(self, power: float, modulo=None):
        return Power(self,power)

    def NR_evaluate(self, assgms:Assignments, epsilon: int = 0.0001, times: int = 100):
        xn = 20
        # f = lambda x: Constant(self.coefs[2]) * (self.v ** float(2)) + Constant(self.coefs[1]) * self.v + Constant(self.coefs[0])
        print(type(assgms))
        if isinstance(assgms,Assignment):
            return True
        return False
        # df=self.derivative(self.v)
        # print(df)
        # print(self.evaluate(assgms))
        # for n in range(0, times):
        #     fxn = self.evaluate(assgms)
        #     print(fxn)
        #     if abs(fxn) < epsilon:
        #         print('Found solution after', n, 'iterations.')
        #         return xn
        #     dfxn = df(xn)
        #     if dfxn == 0:
        #         print('Zero derivative. No solution found.')
        #         return None
        #     xn = xn - fxn / dfxn
        # print('Exceeded maximum iterations. No solution found.')
        # return None





#
# x = VariableExpression("x")
# y = VariableExpression("y")
# z = VariableExpression("z")
# print(x == y)
# print(x == x)
# ass1 = ValueAssignment(x, 10)
# ass2 = ValueAssignment(y, 20)
# sda = SimpleDictionaryAssignments()
# sda += ass1
# sda += ass2
# print(ass1)
# print(ass2)
# print(ass1)
# print(ass2)
# print(x)
# print(x.evaluate(sda))
# print(y)
# print(y.evaluate(sda))
# try:
#     print(z.evaluate(sda))
# except:
#     print("no assignment for all variables")
#
# print("--- cons ---")
# con0 = Constant(0.0)
# con1 = Constant(1.0)
# con2 = Constant(2.0)
# print(con0)
# print(con0.evaluate(sda))
# # print(con0.evaluate())
# print(con0 == con1)
# print(con0 == x)
# print(con0 == con0)
# print(con1)
# print(con2)
#
# print("--- add ---")
# add = x + y
# print(add)
# print(add.evaluate(sda))
# print(add.derivative(x))
# print(add.derivative(y))
# print(add.derivative(z))
# print(add.derivative(x).evaluate(sda))
# print(add == x)
#
# print("--- sub ---")
# sub = x-y
# sub2 = x - z + y
# print(sub)
# print(sub.evaluate(sda))
# print(sub.derivative(x))
# print(sub.derivative(y))
# print(sub.derivative(z))
# print(sub2 == sub)
#
# try:
#     print(sub2.evaluate(sda))
# except:
#     print("no assignment for all variables")
#
# print("--- mul 1 ---")
# mul1 = x * y
# mul2 = z * y
# print(mul1)
# print(mul1.evaluate(sda))
# print(mul1.derivative(x))
# print(mul1.derivative(y))
# print(mul1.derivative(z))
# print(mul1.derivative(x).evaluate(sda))
# print(mul2)
# try:
#     print(mul2.evaluate(sda))
# except:
#     print("no assignment for all variables")
#
# print("--- comp 2 ---")
#
# comp2 = add * sub
# print(type(comp2))
# print(comp2)
# print(comp2.evaluate(sda))
# print(comp2.derivative(x))
# print(comp2.derivative(x).evaluate(sda))
# print(comp2.derivative(x).derivative(x))
#
# print("--- power 1 ---")
# pow1 = add ** 3
#
# print(pow1)
# print(pow1.evaluate(sda))
# print(pow1.derivative(x))
# print(pow1.derivative(x).evaluate(sda))
# print("--- complex ---")
# complex = ((x+y)*(y+x))**3.0
# print(complex)
# print(complex.derivative(x))
#
#
#
# print("--- Poly 1 ---")
# print(Polynomial(x, [12,-8,-1]))
# print(Polynomial(x, [0,0,-1]))
# print(Polynomial(x, [-2,0,0]))
# pol = Polynomial(x, [12,8,1])
# print(pol)
# print(pol.derivative(x))
# print(pol.derivative(y))
# v =pol.NR_evaluate(ValueAssignment(x,0.5), 0.01, 1000)
# print(v)
# print(pol.evaluate(sda))
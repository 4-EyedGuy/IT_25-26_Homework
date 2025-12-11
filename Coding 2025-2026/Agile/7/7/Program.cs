using PayrollSystem;
using PayrollSystem.Rules;

var calculator = new PayrollCalculator();
var context = new PayrollContext
{
    Base = 50000,
    Bonus = 15000,
    Penalty = 5000
};

SalaryRule applyPenalty = ctx =>
{
    ctx.Final -= ctx.Penalty;
    Console.WriteLine("ApplyPenalty: применено");
};

Console.WriteLine("<< Подписка на правила >>");
calculator.Rules += AddBaseRule.Execute;
calculator.Rules += AddBonusRule.Execute;
calculator.Rules += applyPenalty;

calculator.Run(context);

Console.WriteLine("\n<< Отписка от штрафа >>");
calculator.Rules -= applyPenalty;

context = new PayrollContext
{
    Base = 50000,
    Bonus = 15000,
    Penalty = 5000
};

calculator.Run(context);
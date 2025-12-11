namespace PayrollSystem.Rules;

using PayrollSystem;

public static class AddBonusRule
{
    public static void Execute(PayrollContext ctx)
    {
        ctx.Final += ctx.Bonus;
        Console.WriteLine("AddBonus: применено");
    }
}
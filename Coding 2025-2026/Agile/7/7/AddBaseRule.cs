namespace PayrollSystem.Rules;

using PayrollSystem;

public static class AddBaseRule
{
    public static void Execute(PayrollContext ctx)
    {
        ctx.Final += ctx.Base;
        Console.WriteLine("AddBase: применено");
    }
}
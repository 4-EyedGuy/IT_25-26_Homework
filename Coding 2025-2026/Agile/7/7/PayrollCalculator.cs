namespace PayrollSystem;

public class PayrollCalculator
{
    public event SalaryRule? Rules;

    public void Run(PayrollContext context)
    {
        context.Final = 0;
        Rules?.Invoke(context);
        Console.WriteLine($"Расчёт завершён: {context}");
    }
}
export default function FormulaBlock({ formulas }: { formulas: string[] }) {
  return (
    <div className="formula-list">
      {formulas.map((formula) => (
        <code key={formula}>{formula}</code>
      ))}
    </div>
  );
}

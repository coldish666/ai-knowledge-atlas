export default function StatusBadge({ value }: { value: string }) {
  const className = value === "已完成" || value === "已掌握" ? "badge done" : value === "进行中" || value === "模糊" ? "badge doing" : "badge";
  return <span className={className}>{value}</span>;
}

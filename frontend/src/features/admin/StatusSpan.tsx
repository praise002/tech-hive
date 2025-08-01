interface StatusSpanProps {
  status: string;
}

function StatusSpan({ status }: StatusSpanProps) {
  return (
    <span
      className={`lg:px-5 px-2 py-3 rounded-md ${
        status === 'Active' || status === 'Published'
          ? 'bg-mint text-custom-green'
          : 'bg-cream text-red'
      }`}
    >
      {status}
    </span>
  );
}

export default StatusSpan;

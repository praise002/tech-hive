interface RoleSpanProps {
  role: string;
}

function RoleSpan({ role }: RoleSpanProps) {
  return (
    <span className="lg:px-5 px-2 py-3 rounded-md bg-cream text-orange-dark">
      {role}
    </span>
  );
}

export default RoleSpan;

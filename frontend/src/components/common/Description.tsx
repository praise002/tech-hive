import { DescriptionProps } from "../../types";

function Description({ children }: DescriptionProps) {
  return (
    <p className="text-primary dark:text-custom-white text-sm md:text-base">
      {children}
    </p>
  );
}

export default Description;

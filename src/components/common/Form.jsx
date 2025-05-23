import { useForm } from 'react-hook-form';
import PropTypes from 'prop-types';
import Button from './Button';

function Form({ inputs, onSubmit, children, onClick, className }) {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm();

  // Handle form submission
  function submitForm(data) {
    if (onSubmit) {
      onSubmit(data, reset); // Call the parent's onSubmit function
    }
  }

  return (
    <form onSubmit={handleSubmit(submitForm)}>
      {/* Dynamically render inputs based on the 'inputs' prop */}
      {inputs.map((input, index) => (
        <div key={index} className="relative mb-4">
          {/* Render the input field */}
          <input
            {...register(input.name, input.rules)} // Apply validation rules
            id={input.id || input.name}
            placeholder={input.placeholder || ''}
            type={input.type || 'text'}
            className="appearance-none block w-full px-4 py-2 border border-gray-300 rounded-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-800 focus-visible:border-gray-800"
          />

          {input.icon && (
            <button type='button' 
            onClick={input.onIconClick}
            aria-label={input.iconAriaLabel || 'Toggle field options'}
            className="absolute right-3 top-1/2 -translate-y-1/2">
              {input.icon}
            </button>
          )}

          {/* Render error messages if validation fails */}
          {errors[input.name] && (
            <p className="text-red-500 text-sm mt-1">
              {errors[input.name]?.message}
            </p>
          )}
        </div>
      ))}

      {/* Submit button */}
      <Button type="submit" onClick={onClick} className={className}>
        {children}
      </Button>
    </form>
  );
}

Form.propTypes = {
  inputs: PropTypes.arrayOf(
    PropTypes.shape({
      name: PropTypes.string.isRequired,
      placeholder: PropTypes.string,
      type: PropTypes.string,
      rules: PropTypes.object,
      id: PropTypes.string,
      onIconClick: PropTypes.func, 
      iconAriaLabel: PropTypes.string,
    })
  ).isRequired, // The inputs array is required
  onSubmit: PropTypes.func,
  children: PropTypes.node.isRequired,
  onClick: PropTypes.func,
  className: PropTypes.string,
};

export default Form;

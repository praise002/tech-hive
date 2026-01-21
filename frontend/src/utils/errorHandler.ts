import { UseFormSetError } from 'react-hook-form';

/**
 * Handles mutation errors from the backend API
 * Backend error structure:
 * - With field errors: { err_code, status, message, data: { field: error } }
 * - Without field errors: { err_code, status, message }
 */
export function handleMutationError(
  error: any,
  setError?: UseFormSetError<any>,
  fieldMapping?: Record<string, string>
): string {
  // Handle field-specific errors if setError is provided
  if (error.data && setError) {
    Object.entries(error.data).forEach(([field, message]) => {
      const formField = fieldMapping?.[field] || field;
      setError(formField, {
        type: 'server',
        message: Array.isArray(message) ? message[0] : String(message),
      });
    });
  }

  return error.message || 'An error occurred. Please try again.';
}

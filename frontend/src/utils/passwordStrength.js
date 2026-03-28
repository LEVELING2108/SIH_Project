/**
 * Password Strength Validator Hook
 */
export function usePasswordStrength() {
  const validatePassword = (password) => {
    const errors = [];
    let score = 0;

    if (!password) {
      return { isValid: false, errors: ['Password is required'], score: 0, level: 'weak' };
    }

    // Check minimum length
    if (password.length < 8) {
      errors.push('Password must be at least 8 characters');
    } else {
      score += 20;
      if (password.length >= 12) score += 10;
      if (password.length >= 16) score += 10;
    }

    // Check for uppercase
    if (/[A-Z]/.test(password)) {
      score += 15;
    } else {
      errors.push('Password must contain at least one uppercase letter');
    }

    // Check for lowercase
    if (/[a-z]/.test(password)) {
      score += 15;
    } else {
      errors.push('Password must contain at least one lowercase letter');
    }

    // Check for digit
    if (/[0-9]/.test(password)) {
      score += 15;
    } else {
      errors.push('Password must contain at least one number');
    }

    // Check for special character
    if (/[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\;'\`~]/.test(password)) {
      score += 15;
    } else {
      errors.push('Password must contain at least one special character (!@#$%^&*...)');
    }

    // Check for common passwords
    const commonPasswords = ['password', '123456', 'qwerty', 'admin', 'letmein', 'welcome', 'monkey', 'dragon'];
    if (commonPasswords.includes(password.toLowerCase())) {
      errors.push('Password is too common. Please choose a stronger password');
      score = Math.max(0, score - 30);
    }

    // Check for sequential characters
    if (/(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)/.test(password.toLowerCase())) {
      score = Math.max(0, score - 10);
    }

    const level = score <= 40 ? 'weak' : score <= 70 ? 'medium' : 'strong';

    return {
      isValid: errors.length === 0,
      errors,
      score: Math.min(100, score),
      level
    };
  };

  return { validatePassword };
}

/**
 * Password Strength Indicator Component
 */
export function PasswordStrengthIndicator({ password }) {
  const { validatePassword } = usePasswordStrength();
  const result = validatePassword(password);

  if (!password) return null;

  const getStrengthColor = (level) => {
    switch (level) {
      case 'weak': return '#ff4757';
      case 'medium': return '#ffa502';
      case 'strong': return '#2ed573';
      default: return '#ccc';
    }
  };

  const getStrengthLabel = (level) => {
    switch (level) {
      case 'weak': return '🔴 Weak';
      case 'medium': return '🟡 Medium';
      case 'strong': return '🟢 Strong';
      default: return '';
    }
  };

  return (
    <div style={{ marginTop: '0.5rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
        <span style={{ fontSize: '0.85rem', color: '#666' }}>Password Strength</span>
        <span style={{ fontSize: '0.85rem', fontWeight: '600', color: getStrengthColor(result.level) }}>
          {getStrengthLabel(result.level)}
        </span>
      </div>
      <div style={{
        width: '100%',
        height: '6px',
        background: '#e0e0e0',
        borderRadius: '3px',
        overflow: 'hidden'
      }}>
        <div style={{
          width: `${result.score}%`,
          height: '100%',
          background: getStrengthColor(result.level),
          transition: 'width 0.3s ease'
        }} />
      </div>
      {result.errors.length > 0 && (
        <ul style={{
          marginTop: '0.5rem',
          paddingLeft: '1.25rem',
          fontSize: '0.8rem',
          color: '#ff4757'
        }}>
          {result.errors.map((error, idx) => (
            <li key={idx}>{error}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

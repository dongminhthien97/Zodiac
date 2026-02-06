/**
 * Validates the astrology profile data structure.
 * 
 * @param {Object} data - The API response data to validate
 * @returns {Object} - Result object with isValid boolean and errors array
 */
export const validateContent = (data) => {
    const errors = []

    if (!data) {
        return { isValid: false, errors: ['Missing data'] }
    }

    // Validate meta
    if (!data.meta) {
        errors.push('Missing "meta" field')
    } else if (!data.meta.house_system_used) {
        errors.push('Missing "house_system_used" in meta')
    } else if (!['whole_sign', 'placidus', 'both'].includes(data.meta.house_system_used)) {
        errors.push(`Invalid house_system_used: ${data.meta.house_system_used}`)
    }

    // Validate sections
    if (!data.sections) {
        errors.push('Missing "sections" field')
    } else {
        // Check for at least one valid section or typical sections if strict validation needed
        // For now, we just ensure sections object exists
        if (Object.keys(data.sections).length === 0) {
            errors.push('Sections object is empty')
        }
    }

    return {
        isValid: errors.length === 0,
        errors
    }
}

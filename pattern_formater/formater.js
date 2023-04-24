function patternFormater(str, pattern, removeSpaces = false) {
    // Remove whitespaces if specified
    if (removeSpaces) {
        str = str.replace(/\s+/g, '');
    }

    // Build a regex pattern from the provided format string
    let regex = '^';
    for (let i = 0; i < pattern.length; i++) {
        switch (pattern[i]) {
            case 'a':
                regex += '[\\w]';
                break;
            case 'l':
                regex += '[a-zA-Z]';
                break;
            case 'd':
                regex += '\\d';
                break;
            case '*':
                regex += '[\\s\\S]*';
                break;
            default:
                // Remove non-pattern character
                break;
        }
    }
    regex += '$';

    // Test if the string matches the regex pattern
    if (!new RegExp(regex).test(str)) {
        return null;
    }

    // Format the string using the provided pattern
    let formatted = '';
    let index = 0;
    for (let i = 0; i < pattern.length; i++) {
        switch (pattern[i]) {
            case 'a':
                while (index < str.length && !/\w/.test(str[index])) {
                    index++;
                }
                if (index < str.length) {
                    formatted += str[index];
                    index++;
                }
                break;
            case 'l':
                while (index < str.length && !/[a-zA-Z]/.test(str[index])) {
                    index++;
                }
                if (index < str.length) {
                    formatted += str[index].toLowerCase();
                    index++;
                }
                break;
            case 'd':
                while (index < str.length && !/\d/.test(str[index])) {
                    index++;
                }
                if (index < str.length) {
                    formatted += str[index];
                    index++;
                }
                break;
            case '*':
                formatted += str.substr(index);
                index = str.length;
                break;
            default:
                formatted += pattern[i];
                break;
        }
        if (index >= str.length) {
            break;
        }
    }

    return formatted;
}

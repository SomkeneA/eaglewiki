document.addEventListener("DOMContentLoaded", function() {
    function parseDate(dateString) {
        const parts = dateString.split("-");
        return new Date(parts[0], parts[1] - 1, parts[2]);
    }

    function calculateAge(birthDate) {
        const today = new Date();
        const birth = parseDate(birthDate);
        let age = today.getFullYear() - birth.getFullYear();
        const monthDifference = today.getMonth() - birth.getMonth();

        if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < birth.getDate())) {
            age--;
        }

        return age;
    }

    const birthDateElement = document.getElementById('birth-date-placeholder');
    const birthDate = birthDateElement.textContent.trim();

    if (birthDate) {
        const age = calculateAge(birthDate);
        birthDateElement.textContent = `${birthDate} (Age: ${age})`;
    }
});

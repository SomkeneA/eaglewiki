document.addEventListener('DOMContentLoaded', function () {
    const entryLists = document.querySelectorAll('.entry_list');
    if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        addAnimation();
    }

    function addAnimation() {
        entryLists.forEach(entryList => {
            entryList.setAttribute("data-animated", "true");

            const scrollerList = entryList.querySelector('.list');
            const scrollerInnerList = Array.from(scrollerList.children);

            scrollerInnerList.forEach(item =>{
                const duplicatedItem = item.cloneNode(true);
                duplicatedItem.setAttribute("aria-hidden", true);
                scrollerList.appendChild(duplicatedItem);
            })
        });
    }
});
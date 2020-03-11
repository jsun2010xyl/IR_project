let res = '';
document.querySelectorAll('.c-list__title')
    .forEach((node) => {
        const text = node.innerHTML;
        res += node.innerHTML.substring(text.indexOf('‘') + 1, text.lastIndexOf('’'));
        res += '\n';
    })
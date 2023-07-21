import createHistory from 'history/createHashHistory';
let thisHistory = createHistory()
thisHistory.listen((location) => {
    setTimeout(() => {
        if (location.action === 'POP') return;
        window.scrollTo(0, 0);
    });
});

export default thisHistory;



export let uid = () => {
    const now = +(new Date());
    return `bee-${now}`;
};

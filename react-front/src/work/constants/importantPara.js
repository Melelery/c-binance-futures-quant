export const appVersion = "1393";
let initSystemType = "android"
if(process.env.NODE_ENV=="development"){
    initSystemType = "android"
}

export const systemType = initSystemType;//ios or android

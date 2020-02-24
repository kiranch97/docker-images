export function formatDate(date) {
    let year = date.getFullYear();
    let month = this.addZero(date.getMonth() + 1);
    let day = this.addZero(date.getDate());
    let hour = this.addZero(date.getHours());
    let min = this.addZero(date.getMinutes());
    let sec = this.addZero(date.getSeconds());
    let millisec = this.addZeroMillisec(date.getMilliseconds());

    this.timeFormat = `${year}-${month}-${day} ${hour}:${min}:${sec}.${millisec}`;

    return this.timeFormat;
}

// ----

export function todayDateFunc(date) {
    let year = date.getFullYear();
    let month = this.addZero(date.getMonth() + 1);
    let day = this.addZero(date.getDate());

    this.todayDate = year + "-" + month + "-" + day;

    return this.todayDate;
}

// ----

export function addZero(i) {
    if (i < 10) {
        i = "0" + i;
    }
    return i;
}

// ----

export function addZeroMillisec(i) {
    if (i < 100) {
        i = "00" + i;
    } else if (i >= 100 < 1000) {
        i = "0" + i;
    }
    return i;
}

// ----
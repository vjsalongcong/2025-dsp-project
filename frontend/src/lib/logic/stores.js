import { writable } from 'svelte/store';

export const timestampValue = writable(null);
export const iaqStatus = writable(null);

export const calibrationValues = writable({
    "temperature": "",
    "humidity": "",
    "carbon_dioxide": "",
    "carbon_monoxide": "",
    "nitrogen_dioxide": "",
    "ammonia": ""
});

export const thresholdValues = writable({
    "max-temperature": "",
    "min-temperature": "",
    "max-humidity": "",
    "min-humidity": "",
    "carbon_dioxide": "",
    "carbon_monoxide": "",
    "nitrogen_dioxide": "",
    "ammonia": ""
});

export const mqttValues = writable({
    "broker": "",
    "port": "",
    "topic": "",
    "username": "",
    "password": ""
});
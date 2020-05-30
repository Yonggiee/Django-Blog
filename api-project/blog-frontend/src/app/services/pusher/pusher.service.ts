import { Injectable } from '@angular/core';
import Pusher from 'pusher-js';

@Injectable({
  providedIn: 'root',
})
export class PusherService {
  pusher: any;

  constructor() {
    this.pusher = new Pusher('abba23015c83be9e8d00', {
      cluster: 'ap1',
    });
  }
}

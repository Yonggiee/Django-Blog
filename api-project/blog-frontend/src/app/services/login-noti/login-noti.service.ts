import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LoginNotiService {
  private logger = new Subject<boolean>();
  notiService = this.logger.asObservable();
  isLogged: boolean = false;

  constructor() { }

  triggerService() {
    if (localStorage.hasOwnProperty('refreshToken')) {
      this.isLogged = true;
    } else {
      this.isLogged = false;
    }
    this.logger.next(this.isLogged);
  }
}

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { baseurl, httpOptions } from '../commons.service';
import { LoginNotiService } from '../login-noti/login-noti.service';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  errors: any = [];

  constructor(
    private http: HttpClient,
    private loginNotiService: LoginNotiService
  ) {}

  // Uses http.post() to get an auth token from djangorestframework-jwt endpoint
  public login(user) {
    this.http
      .post(baseurl + '/api/token/', user, httpOptions)
      .subscribe(
        (data) => {
          this.updateAfterLogin(data);
          this.loginNotiService.triggerService();
        },
        (err) => {
          this.errors = err['error'];
        }
      );
  }

  public logout() {
    localStorage.clear();
    this.loginNotiService.triggerService();
  }

  private updateAfterLogin(data) {
    const accessToken = data['access'];
    const refreshToken = data['refresh'];
    this.updateAccess(accessToken);
    this.updateRefresh(refreshToken);
  }

  private updateAccess(token){
    localStorage.setItem('accessToken', token);
    this.errors = [];
  }

  private updateRefresh(token){
    localStorage.setItem('refreshToken', token);
    this.errors = [];
  }

}

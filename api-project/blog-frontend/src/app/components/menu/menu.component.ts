import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { LoginComponent } from '../login/login.component';
import { LoginNotiService } from 'src/app/services/login-noti/login-noti.service';
import { UserService } from 'src/app/services/user/user.service';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.css'],
})
export class MenuComponent implements OnInit {
  public isLogged: boolean = false;

  constructor(
    private dialog: MatDialog,
    private userService: UserService,
    private loginNotiService: LoginNotiService
  ) {}

  ngOnInit(): void {
    if (localStorage.hasOwnProperty('refreshToken')) {
      this.isLogged = true;
    }
    this.loginNotiService.notiService
      .subscribe(isLogged => {
        this.isLogged = isLogged;
        this.ngOnInit();
      })
  }

  openLoginMenu() {
    this.dialog.open(LoginComponent);
  }

  logout() {
    this.userService.logout();
  }
}

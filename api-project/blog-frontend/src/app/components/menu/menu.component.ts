import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { LoginComponent } from '../login/login.component';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.css'],
})
export class MenuComponent implements OnInit {
  public isLogged: boolean = false;

  constructor(private dialog: MatDialog) {}

  ngOnInit(): void {
    if (localStorage.hasOwnProperty('refreshToken')) {
      this.isLogged = true;
    }
  }

  openLoginMenu() {
    this.dialog.open(LoginComponent);
  }
}

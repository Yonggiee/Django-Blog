import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { Validators } from '@angular/forms';
import { UserService } from 'src/app/services/user.service';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent implements OnInit {
  username: String;

  loginForm = new FormGroup({
    username: new FormControl('', Validators.required),
    password: new FormControl('', Validators.required),
  });

  constructor(
    private dialogRef: MatDialogRef<LoginComponent>, 
    private loginService: UserService
  ) {}

  ngOnInit(): void {}

  onSubmit() {
    let loginDetails = this.loginForm.value;
    this.loginService.login(loginDetails);
    this.username = this.loginForm.get('username').value;
    this.dialogRef.close([]);
  }
}

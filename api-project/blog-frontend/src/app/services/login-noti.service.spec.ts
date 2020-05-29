import { TestBed } from '@angular/core/testing';

import { LoginNotiService } from './login-noti.service';

describe('LoginNotiService', () => {
  let service: LoginNotiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LoginNotiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

import { HttpHeaders } from '@angular/common/http';
export const baseurl = 'http://0.0.0.0:8000';
export const httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
};
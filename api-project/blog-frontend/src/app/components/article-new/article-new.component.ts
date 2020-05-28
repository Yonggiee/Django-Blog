import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { Validators } from '@angular/forms';
import { ArticleService } from 'src/app/services/article.service';

@Component({
  selector: 'app-article-new',
  templateUrl: './article-new.component.html',
  styleUrls: ['./article-new.component.css'],
})
export class ArticleNewComponent implements OnInit {
  articleForm = new FormGroup({
    title: new FormControl('', Validators.required),
    desc: new FormControl('', Validators.required),
    user: new FormControl(''),
  });

  constructor(private articleService: ArticleService) {}

  ngOnInit(): void {}

  onSubmit() {
    let newArticle = this.articleForm.value;
    this.articleService.postArticle(newArticle).subscribe(
      data => {
        newArticle = data;
      }
    );
  }
}

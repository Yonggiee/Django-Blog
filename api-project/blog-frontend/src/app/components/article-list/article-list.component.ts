import { Component, OnInit, OnDestroy } from '@angular/core';
import { MatDialogModule, MatDialog } from '@angular/material/dialog';
import { ArticleService } from 'src/app/services/article/article.service';
import { ArticleNewComponent } from '../article-new/article-new.component';
import { PusherService } from 'src/app/services/pusher/pusher.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-article-list',
  templateUrl: './article-list.component.html',
  styleUrls: ['./article-list.component.css'],
})
export class ArticleListComponent implements OnInit, OnDestroy {
  articleSubscription: Subscription;
  articles;

  constructor(
    private articleService: ArticleService,
    private pusherService: PusherService,
    private dialog: MatDialog
  ) {}
  ngOnInit(): void {
    this.getArticles();
    this.subscribeToArticlesChannel();
  }

  ngOnDestroy(): void {
    this.articleSubscription.unsubscribe();
  }

  getArticles() {
    this.articleSubscription = this.articleService.getAllArticles().subscribe((articles) => {
      this.articles = articles;
    });
  }

  newArticle() {
    this.dialog.open(ArticleNewComponent);
  }

  subscribeToArticlesChannel() {
    const component = this;
    const channel = this.pusherService.pusher.subscribe('blog');
    channel.bind('refresh-articles', function () {
      component.getArticles();
    });
  }
}

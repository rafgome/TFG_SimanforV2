import { Component } from "@angular/core";
import { TranslateService } from "@ngx-translate/core";
import { Subscription } from "rxjs/internal/Subscription";
import { CommonService } from "./../../../_services/common.service";
import { ConfirmationComponent } from "../../../pages/utils/confirmation/confirmation.component";
import { MatDialog } from "@angular/material";
import { AuthService } from "../../../_services/auth.service";
import { Router } from "@angular/router";

@Component({
  selector: "app-header",
  templateUrl: "./header.component.html",
  styleUrls: ["./header.component.css"],
})
export class AppHeaderComponent {
  loaderState: boolean;
  loadetText: string;
  subscriptionLoader: Subscription;

  constructor(
    public translate: TranslateService,
    public dialog: MatDialog,
    public authService: AuthService,
    public router: Router,
    private commonService: CommonService
  ) {}

  ngOnInit() {
    this.subscriptionLoader = this.commonService.loader$.subscribe(
      (loaderstate) => {
        this.loaderState = loaderstate.state;
        this.loadetText = loaderstate.text;
      }
    );
  }

  ngOnDestroy() {
    this.subscriptionLoader.unsubscribe();
  }

  switchLang(ob) {
    window.localStorage.setItem("language", ob.value);
    this.translate.use(ob.value);
  }

  closeSession() {
    const confirmation = this.dialog.open(ConfirmationComponent);
    confirmation.componentInstance.message = "menu.close_session_confirmation";
    confirmation.afterClosed().subscribe((result) => {
      if (result) {
        this.authService.logout();
        this.router.navigate(["/"]);
      }
    });
  }
}

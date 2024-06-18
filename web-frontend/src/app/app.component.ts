import { Component, OnDestroy, OnInit } from "@angular/core";
import { TranslateService, LangChangeEvent } from "@ngx-translate/core";
import {
  NgcCookieConsentService,
  NgcInitializeEvent,
  NgcNoCookieLawEvent,
  NgcStatusChangeEvent,
} from "ngx-cookieconsent";
import { Subscription } from "rxjs";

@Component({
  selector: "app-root",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.css"],
})
export class AppComponent implements OnInit, OnDestroy {
  // keep refs to subscriptions to be able to unsubscribe later
  private popupOpenSubscription: Subscription;
  private popupCloseSubscription: Subscription;
  private initializeSubscription: Subscription;
  private statusChangeSubscription: Subscription;
  private revokeChoiceSubscription: Subscription;
  private noCookieLawSubscription: Subscription;

  constructor(
    private translate: TranslateService,
    private ccService: NgcCookieConsentService
  ) {
    this.translate.addLangs(["en", "es", "gl", "fr", "pt", "vi", "eu"]);

    const fallbackLanguages = {
      en: "en",
      es: "en",
      gl: "es",
      fr: "en",
      pt: "en",
      vi: "en",
      eu: "es",
    };

    const storageLanguage = window.localStorage.getItem("language");
    this.translate.use(storageLanguage || "es");

    this.translate.onLangChange.subscribe((event: LangChangeEvent) => {
      this.translate.setDefaultLang(fallbackLanguages[event.lang] || "en");
    });
  }

  ngOnInit() {
    // subscribe to cookieconsent observables to react to main events
    this.popupOpenSubscription = this.ccService.popupOpen$.subscribe(() => {
      // you can use this.ccService.getConfig() to do stuff...
    });

    this.popupCloseSubscription = this.ccService.popupClose$.subscribe(() => {
      // you can use this.ccService.getConfig() to do stuff...
    });

    this.initializeSubscription = this.ccService.initialize$.subscribe(
      (event: NgcInitializeEvent) => {
        // you can use this.ccService.getConfig() to do stuff...
      }
    );

    this.statusChangeSubscription = this.ccService.statusChange$.subscribe(
      (event: NgcStatusChangeEvent) => {
        // you can use this.ccService.getConfig() to do stuff...
      }
    );

    this.revokeChoiceSubscription = this.ccService.revokeChoice$.subscribe(
      () => {
        // you can use this.ccService.getConfig() to do stuff...
      }
    );

    this.noCookieLawSubscription = this.ccService.noCookieLaw$.subscribe(
      (event: NgcNoCookieLawEvent) => {
        // you can use this.ccService.getConfig() to do stuff...
      }
    );

    this.translate
      .get([
        "cookie.header",
        "cookie.message",
        "cookie.dismiss",
        "cookie.allow",
        "cookie.deny",
        "cookie.link",
        "cookie.policy",
      ])
      .subscribe((data) => {
        this.ccService.getConfig().content =
          this.ccService.getConfig().content || {};
        // Override default messages with the translated ones
        this.ccService.getConfig().content.header = data["cookie.header"];
        this.ccService.getConfig().content.message = data["cookie.message"];
        this.ccService.getConfig().content.dismiss = data["cookie.dismiss"];
        this.ccService.getConfig().content.allow = data["cookie.allow"];
        this.ccService.getConfig().content.deny = data["cookie.deny"];
        this.ccService.getConfig().content.link = data["cookie.link"];
        this.ccService.getConfig().content.policy = data["cookie.policy"];

        this.ccService.destroy(); // remove previous cookie bar (with default messages)
        this.ccService.init(this.ccService.getConfig()); // update config with translated messages
      });
  }

  ngOnDestroy() {
    // unsubscribe to cookieconsent observables to prevent memory leaks
    this.popupOpenSubscription.unsubscribe();
    this.popupCloseSubscription.unsubscribe();
    this.initializeSubscription.unsubscribe();
    this.statusChangeSubscription.unsubscribe();
    this.revokeChoiceSubscription.unsubscribe();
    this.noCookieLawSubscription.unsubscribe();
  }
}

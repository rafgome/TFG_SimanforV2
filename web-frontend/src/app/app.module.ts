import { BrowserModule } from "@angular/platform-browser";
import { NgModule } from "@angular/core";
import { RouterModule } from "@angular/router";
import { FormsModule } from "@angular/forms";
import { HttpClientModule, HttpClient } from "@angular/common/http";
import { LocationStrategy, PathLocationStrategy } from "@angular/common";
import { AppRoutes } from "./app.routing";
import { AppComponent } from "./app.component";

import { FlexLayoutModule } from "@angular/flex-layout";
import { FullComponent } from "./layouts/full/full.component";
import { AppHeaderComponent } from "./layouts/full/header/header.component";
import { AppSidebarComponent } from "./layouts/full/sidebar/sidebar.component";
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { DemoMaterialModule } from "./demo-material-module";

import { SharedModule } from "./shared/shared.module";
import { SpinnerComponent } from "./shared/spinner.component";

// import ngx-translate and the http loader
import { TranslateLoader, TranslateModule } from "@ngx-translate/core";
import { TranslateHttpLoader } from "@ngx-translate/http-loader";
import "@angular/localize/init";
import { ApiService } from "./_services/api.service";
import { JwtModule } from "@auth0/angular-jwt";
import { HomeComponent } from "./pages/home/home.component";
import {
  NgcCookieConsentModule,
  NgcCookieConsentConfig,
} from "ngx-cookieconsent";

const cookieConfig: NgcCookieConsentConfig = {
  cookie: {
    domain: window.location.hostname,
  },
  position: "bottom",
  theme: "classic",
  palette: {
    popup: {
      background: "#91b450",

      text: "#ffffff",
      link: "#ffffff",
    },
    button: {
      background: "#ffffff",
      text: "#000000",
      border: "transparent",
    },
  },
  type: "info",
  content: {
    href: "/cookies",
  },
};

@NgModule({
  declarations: [
    AppComponent,
    FullComponent,
    AppHeaderComponent,
    SpinnerComponent,
    AppSidebarComponent,
    HomeComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    DemoMaterialModule,
    FormsModule,
    FlexLayoutModule,
    HttpClientModule,
    SharedModule,
    RouterModule.forRoot(AppRoutes),
    TranslateModule.forRoot({
      loader: {
        provide: TranslateLoader,
        useFactory: HttpLoaderFactory,
        deps: [HttpClient],
      },
    }),
    JwtModule.forRoot({
      config: {
        tokenGetter: tokenGetter,
        whitelistedDomains: [],
        blacklistedRoutes: [],
      },
    }),
    NgcCookieConsentModule.forRoot(cookieConfig),
  ],
  providers: [
    { provide: LocationStrategy, useClass: PathLocationStrategy },
    ApiService,
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}

export function tokenGetter() {
  return localStorage.getItem("authToken");
}

export function HttpLoaderFactory(http: HttpClient) {
  return new TranslateHttpLoader(http);
}

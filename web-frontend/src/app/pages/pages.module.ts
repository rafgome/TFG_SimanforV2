import "hammerjs";
import { NgModule } from "@angular/core";
import { RouterModule } from "@angular/router";
import { HttpClientModule } from "@angular/common/http";
import { CommonModule } from "@angular/common";

import { DemoMaterialModule } from "../demo-material-module";
import { CdkTableModule } from "@angular/cdk/table";

import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { FlexLayoutModule } from "@angular/flex-layout";

import { MaterialRoutes } from "./pages.routing";
import { LoginComponent } from "./login/login.component";
import {
  ModelsComponent,
  DialogOverviewExampleDialogComponent,
} from "./models/models.component";
import { InventoryComponent } from "./inventory/inventory.component";

import { DataTablesModule } from "angular-datatables";
import { TranslateModule } from "@ngx-translate/core";
import {
  TableComponent,
  TableDialogComponent,
} from "./utils/table/table.component";
import { AddElementComponent } from "./utils/add-element/add-element.component";
import { AddScenarioComponent } from "./utils/add-scenario/add-scenario.component";
import { AddActionComponent } from "./utils/add-action/add-action.component";
import { ShowActionComponent } from "./utils/show-action/show-action.component";
import { ScenariosComponent } from "./scenarios/scenarios.component";
import { UsersComponent } from "./users/users.component";
import { ConfirmationComponent } from "./utils/confirmation/confirmation.component";
import { CutterPipe } from "../../pipes/cutter.pipe";
import { HelpComponent } from "./help/help.component";
import { LegalComponent } from "./legal/legal.component";
import { CookiesComponent } from "./cookies/cookies.component";
import { DigitOnlyDirective } from "./utils/directives/digit-only.directive";
import { BasicSpinner } from "./utils/basic-spinner/basic-spinner.component";
import { ActionsComponent } from "./actions/actions.component";
import { ResultsComponent } from "./utils/results/results.component";

@NgModule({
  imports: [
    CommonModule,
    RouterModule.forChild(MaterialRoutes),
    DemoMaterialModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    FlexLayoutModule,
    CdkTableModule,
    TranslateModule,
    DataTablesModule,
  ],
  providers: [],
  entryComponents: [DialogOverviewExampleDialogComponent],
  declarations: [
    InventoryComponent,
    ActionsComponent,
    UsersComponent,
    ModelsComponent,
    DialogOverviewExampleDialogComponent,
    TableComponent,
    TableDialogComponent,
    ConfirmationComponent,
    AddElementComponent,
    AddScenarioComponent,
    AddActionComponent,
    ShowActionComponent,
    ScenariosComponent,
    LoginComponent,
    CutterPipe,
    HelpComponent,
    LegalComponent,
    CookiesComponent,
    DigitOnlyDirective,
    BasicSpinner,
    ResultsComponent
  ],
})
export class PagesComponentsModule {}

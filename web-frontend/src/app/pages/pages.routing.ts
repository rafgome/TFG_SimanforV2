import { Routes } from "@angular/router";

import { InventoryComponent } from "./inventory/inventory.component";
import { ActionsComponent } from "./actions/actions.component";
import { UsersComponent } from "./users/users.component";
import { ModelsComponent } from "./models/models.component";
import { ScenariosComponent } from "./scenarios/scenarios.component";
import { LoginComponent } from "./login/login.component";
import { AuthGuardService as AuthGuard } from "../_services/auth-guard.service";
import { HelpComponent } from "./help/help.component";
import { LegalComponent } from "./legal/legal.component";
import { CookiesComponent } from "./cookies/cookies.component";

export const MaterialRoutes: Routes = [
  {
    path: "inventory",
    component: InventoryComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "actions",
    component: ActionsComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "scenarios",
    component: ScenariosComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "models",
    component: ModelsComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "users",
    component: UsersComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "login",
    component: LoginComponent,
  },
  {
    path: "help",
    component: HelpComponent,
  },
  {
    path: "legal",
    component: LegalComponent,
  },
  {
    path: "cookies",
    component: CookiesComponent,
  },
];

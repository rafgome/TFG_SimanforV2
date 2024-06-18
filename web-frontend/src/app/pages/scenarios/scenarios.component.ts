import { Component, OnInit, ViewChild } from "@angular/core";
import { ScenarioService } from "../../_services/scenario.service";
import { Scenario } from "../../_models/scenario";
import { AddScenarioComponent } from "../utils/add-scenario/add-scenario.component";
import { MatDialog } from "@angular/material";
import { MatSnackBar } from "@angular/material/snack-bar";
import { TranslateService } from "@ngx-translate/core";
import { TableComponent } from "../utils/table/table.component";
import { ResultsComponent } from "../utils/results/results.component";

@Component({
  selector: "app-scenarios",
  templateUrl: "./scenarios.component.html",
  styleUrls: ["./scenarios.component.css"],
})
export class ScenariosComponent implements OnInit {
  scenarios: Scenario[];
  header: string[];
  adBlockerEnabled: boolean;

  @ViewChild(TableComponent)
  private tableComponent: TableComponent;

  constructor(
    private scenarioService: ScenarioService,
    public dialog: MatDialog,
    private snackBar: MatSnackBar,
    private translate: TranslateService
  ) {}

  ngOnInit(): void {
    this.loadTableBody();

    setInterval(() => {
      console.info("Refreshing table data...");
      this.loadTableBody();
    }, 30 * 1000);

    this.header = ["_id", "creatorName", "inventoryName", "modelPath", "modelClass", "status"];
  }

  delete(id): void {
    this.scenarioService.deleteScenario(id).subscribe(
      (resp) => {
        console.log("Delete OK");
        this.loadTableBody();
      },
      (error) => {
        console.log("Delete KO", error.status);
        this._showSnack(
          "Error: " + this.translate.instant("error." + error.error.string_code)
        );
      }
    );
  }

  results(dataModel): void {
    const dialogRef = this.dialog.open(ResultsComponent, {
      data: {},
    });
    
    dialogRef.componentInstance.dataModel = dataModel;

    dialogRef.afterClosed().subscribe(() => {
      this.loadTableBody();
    });
  }

  edit(dataModel): void {
    const dialogRef = this.dialog.open(AddScenarioComponent, {
      data: {},
    });

    if (dataModel) {
      dialogRef.componentInstance.dataModel = dataModel;
    }

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.scenarioService
          .addScenario({
            steps: JSON.stringify(result.steps),
            inventoryId: result.inventory._id,
          })
          .subscribe(
            (resp) => {
              console.log("ADD OK");
            },
            (error) => {
              console.log("ADD KO", error.status);
              this._showSnack(
                "Error: " +
                  this.translate.instant("error." + error.error.string_code)
              );
            }
          );
      }
      this.loadTableBody();
    });
  }

  loadTableBody(): void {
    console.log("Loading data...");
    this.scenarioService.getScenarios().subscribe(
      (resp) => {
        this.scenarios = resp.data;
      },
      (error) => {
        console.error(error.status);
        this._showSnack(
          "Error: " + this.translate.instant("error." + error.error.string_code)
        );
      }
    );
  }

  openAddScenarioDialog(): void {
    const dialogRef = this.dialog.open(AddScenarioComponent, {
      data: {},
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        this.scenarioService
          .addScenario({
            steps: JSON.stringify(result.steps),
            inventoryId: result.inventory._id,
            modelClass: result.projectionModel.modelClass,
            modelPath: result.projectionModel.modelPath,
          })
          .subscribe(
            (resp) => {
              console.log("ADD OK");
            },
            (error) => {
              console.log("ADD KO", error.status);
              this._showSnack(
                "Error: " +
                  this.translate.instant("error." + error.error.string_code)
              );
            }
          );
      }
      this.loadTableBody();
    });
  }

  _showSnack(message: string): void {
    this.snackBar.open(message, "Close", {
      duration: 6000,
      horizontalPosition: "center",
      verticalPosition: "top",
    });
  }
}

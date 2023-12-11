package main

import (
	"fmt"

	"github.com/pulumi/pulumi-gcp/sdk/v6/go/gcp/serviceaccount"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi"
	"github.com/pulumi/pulumi/sdk/v3/go/pulumi/config"
)

func main() {
	pulumi.Run(func(ctx *pulumi.Context) error {
		cfg := config.New(ctx, "")

		// Replace this with your GCP project ID
		projectID := cfg.Require("projectID")

		for i := 0; i < 20; i++ {
			// Generate a unique accountID for each service account
			accountID := fmt.Sprintf("my-service-account-%02d", i)

			_, err := serviceaccount.NewAccount(ctx, accountID, &serviceaccount.AccountArgs{
				AccountId:   pulumi.String(accountID),
				DisplayName: pulumi.String(fmt.Sprintf("My Service Account %02d", i)),
				Project:     pulumi.String(projectID),
			})
			if err != nil {
				return err
			}
		}

		return nil
	})
}

